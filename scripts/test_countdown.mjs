import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const source = fs.readFileSync(new URL("../assets/countdown.js", import.meta.url), "utf8");
const target = "2027-05-19T08:40:00-04:00";

function renderAt(now) {
  const marker = { dataset: { tjstarCountdown: target }, textContent: "" };
  class FixedDate extends Date {
    static now() {
      return Date.parse(now);
    }
  }
  const context = {
    Date: FixedDate,
    Number,
    document: { querySelectorAll: () => [marker] },
    window: { setInterval: () => 1 }
  };
  vm.runInNewContext(source, context);
  return marker.textContent;
}

assert.equal(renderAt("2027-05-18T08:40:00-04:00"), "T−1d 0h 0m");
assert.equal(renderAt("2027-05-19T08:39:00-04:00"), "T−0d 0h 1m");
assert.equal(renderAt("2027-05-19T08:40:00-04:00"), "tjSTAR is today");
assert.equal(renderAt("2027-05-19T23:59:59-04:00"), "tjSTAR is today");
assert.equal(renderAt("2027-05-20T00:00:00-04:00"), "tjSTAR 2027 has concluded");

console.log("Countdown tests passed: before, event day, and next-day states in America/New_York.");
