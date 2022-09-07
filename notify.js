#!/usr/bin/env node
import { writeFileSync } from "node:fs";
import { getReleasesJSON, getUpdatedReleases, sendtoTG } from "./index.js";

const DB_FILE_NAME = "releases.json";
const BOT_API = process.env.BOT_API;
const CHAT_ID = process.env.CHAT_ID;

(async () => {
  const latest = await getReleasesJSON();
  const releases = await getUpdatedReleases(DB_FILE_NAME);
  const res = await sendtoTG(releases, CHAT_ID, BOT_API);

  if (!res) {
    throw new Error(
      "Failed to successfully send notification to telegram. Aborting json file update!"
    );
  }
  // Should always update local releases file after sending notifications
  writeFileSync(DB_FILE_NAME, JSON.stringify(latest, null, 2));
})();
