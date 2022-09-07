import { readFileSync, existsSync } from "node:fs";

/**
 * @param {string} [dbFilePath] - If provided, will try to get `releases` array from it else fetches from upstream (kernel.org)
 * @returns {Promise<Object<string, any>>} JSON object of releases
 */
const getReleasesJSON = async (dbFilePath) => {
  let json = null;
  if (dbFilePath && typeof dbFilePath === "string") {
    if (!existsSync(dbFilePath)) {
      throw new Error(`File does not exists: ${dbFilePath}`);
    }

    try {
      json = JSON.parse(readFileSync(dbFilePath));
      return json;
    } catch (error) {
      throw new Error("Failed to parse local database file!");
    }
  }
  const response = await fetch("https://www.kernel.org/releases.json");
  json = await response.json();
  return json;
};

/**
 * @returns {Promise<Array>} array of updated kernel releases object
 */
const getUpdatedReleases = async (dbFilePath) => {
  const { releases: latestJSON } = await getReleasesJSON();
  const { releases: localJSON } = await getReleasesJSON(dbFilePath);

  if (localJSON) {
    const localVer = new Set();
    localJSON.forEach((rel) => localVer.add(rel.version));
    return latestJSON.filter((rel) => !localVer.has(rel.version));
  }

  return latestJSON;
};

/**
 * @param {Array} releases - array of kernel releases object
 * @returns {Promise<boolean>} `true` if successfully sent, `false` otherwise
 */
const sendtoTG = async (releases, chatID, botAPI) => {
  if (!chatID || !botAPI) {
    // I know I'm bad at phrasing error messages
    throw new Error("CHAT ID or BOT API is not provided!");
  } else if (!releases || !Array.isArray(releases)) {
    throw new Error("No releases array provided!");
  }

  const API_URL = `https://api.telegram.org/bot${botAPI}/sendMessage`;
  const requestBody = Object.assign(Object.create(null), {
    chat_id: chatID,
    parse_mode: "HTML",
  });

  for (const rel of releases) {
    // skip next release updates
    if (rel.moniker === "linux-next") continue;

    const { changelog, diffview: diff, source: tarball, gitweb: browse } = rel;
    const isEOL = rel.iseol ? "[EOL]" : "";

    requestBody.text = `<b>🎉 New kernel release detected!</b>

release: <code>${rel.moniker}</code>
version: <code>${rel.version} ${isEOL}</code>
date: <code>${rel.released.isodate}</code>
patch: <a href="${rel.patch.full}">full</a> | <a href="${rel.patch.incremental}">incremental</a>
`;

    requestBody.reply_markup = { inline_keyboard: [] };
    if (changelog) {
      requestBody.reply_markup.inline_keyboard.push([
        { text: "changelog", url: changelog },
      ]);
    }
    requestBody.reply_markup.inline_keyboard.push([
      { text: "tarball", url: tarball },
    ]);
    requestBody.reply_markup.inline_keyboard.push([
      { text: "diff", url: diff },
    ]);
    requestBody.reply_markup.inline_keyboard.push([
      { text: "browse", url: browse },
    ]);

    // Send the message
    const res = await fetch(API_URL, {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: { "Content-type": "application/json;charset=UTF-8" },
    });

    if (!res.ok) return false;
  }
  return true;
};

export { getReleasesJSON, getUpdatedReleases, sendtoTG };
