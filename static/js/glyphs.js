// Значки тем вместо эмодзи: короткий фрагмент кода на плитке цвета темы.
import { esc } from "./util.js";

const GLYPHS = {
  "py-vars": "x=1", "py-conditions": "if", "py-lists": "[ ]", "py-slices": "[:]",
  "py-functions": "def", "py-for": "for", "py-while": "while", "py-scope": "LEGB",
  "py-tuples": "(,)", "py-dicts": "{k:v}", "py-args": "*args", "py-json": "json",
  "py-comprehensions": "[⋯]", "py-sets": "{ }", "py-sorted": "↑↓", "py-lambda": "λ",
  "py-exceptions": "try", "py-classes": "class", "py-decorators": "@", "py-datetime": "12:00",
  "py-files": "open", "py-context": "with", "py-mutable": "id()", "py-generators": "yield",
  "tools-linux": "$_", "tools-git": "git", "tools-project": "venv",
  "test-pytest": "assert", "test-allure": "report", "test-api": "GET", "test-ui": "</>",
  "test-docker": "FROM", "test-cicd": "CI", "test-kafka": "kafka",
};

// Новая тема без своего значка — первые буквы названия.
export function glyphText(t) {
  return GLYPHS[t.slug] || (t.title || "?").replace(/[^\p{L}\p{N}]/gu, "").slice(0, 2);
}

// Плитка-значок темы. size — сторона в px.
export function glyph(t, size = 54) {
  const text = glyphText(t);
  const fs = Math.round(size * (text.length <= 2 ? 0.42 : text.length <= 4 ? 0.3 : text.length <= 5 ? 0.25 : 0.21));
  return `<span class="glyph" style="--tc:${esc(t.color)};--gs:${size}px;font-size:${fs}px">${esc(text)}</span>`;
}
