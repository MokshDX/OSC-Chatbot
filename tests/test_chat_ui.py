"""Execute the shipped SSE client with a tiny DOM, without a browser dependency."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


def test_complete_replaces_streamed_sentinel_and_removes_sources() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is needed to execute the bundled JavaScript client")
    page = Path("src/osc_assistant/api/static/index.html").read_text(encoding="utf-8")
    script = page.split("<script>", 1)[1].split("</script>", 1)[0]
    harness = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
class Element {
  constructor() { this.children = []; this.listeners = {}; this.writes = []; }
  set textContent(value) { this.text = value; this.writes.push(value); }
  get textContent() { return this.text; }
  appendChild(child) { this.children.push(child); }
  append(...children) { this.children.push(...children); }
  replaceChildren() { this.children = []; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  querySelector() { return null; }
  focus() {}
  scrollIntoView() {}
}
const elements = Object.fromEntries(['log', 'form', 'q', 'send', 'meta'].map(
  id => [id, new Element()]
));
global.document = {
  getElementById: id => elements[id],
  createElement: () => new Element(),
};
global.window = { addEventListener() {} };
const frames = [
  ['sources', [{chunk_id: 'one', title: 'Policy', source_uri: 'fixture', excerpt: 'Data'}]],
  ['delta', {text: '[[NO_'}],
  ['delta', {text: 'ANSWER]]'}],
  ['citation', {chunk_id: 'one'}],
  ['complete', {abstained: true, text: 'No supported answer.', citations: []}],
].map(([name, data]) => `event: ${name}\ndata: ${JSON.stringify(data)}\n\n`);
global.fetch = async url => {
  if (url === '/api/sessions') return {ok: true, json: async () => ({session_id: 'test'})};
  if (url === '/api/health') return {json: async () => ({
    llm: {}, embeddings: {}, vector_store: {},
  })};
  assert.equal(url, '/api/chat');
  let index = 0;
  return {ok: true, body: {getReader: () => ({read: async () =>
    index < frames.length
      ? {done: false, value: new TextEncoder().encode(frames[index++])}
      : {done: true}
  })}};
};
vm.runInThisContext(SOURCE);
(async () => {
  elements.q.value = 'Missing detail?';
  await elements.form.listeners.submit({preventDefault() {}});
  const [, answer, sources] = elements.log.children[0].children;
  assert.ok(answer.writes.includes('[[NO_ANSWER]]'), 'sentinel was provisionally shown');
  assert.equal(answer.textContent, 'No supported answer.');
  assert.equal(answer.className, 'abstained');
  assert.deepEqual(sources.children, []);
  assert.equal(elements.send.disabled, false);
})().catch(error => { console.error(error); process.exitCode = 1; });
"""
    result = subprocess.run(
        [node, "-e", "const SOURCE = " + json.dumps(script) + ";\n" + harness],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr
