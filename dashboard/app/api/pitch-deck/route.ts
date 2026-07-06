import { readFile } from "node:fs/promises";
import path from "node:path";

// Serve the generated report verbatim so it remains a standalone document.

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const deckPath = path.resolve(process.cwd(), "..", "index.html");
    const html = await readFile(deckPath, "utf8");
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  } catch {
    return new Response("Pitch deck has not been generated yet.", {
      status: 404,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
}
