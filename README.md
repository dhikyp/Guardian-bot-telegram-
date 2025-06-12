# Guardian-bot-telegram-
Bot anti phising telegram 
python-telegram-bot==13.15
Flask
// main.ts
import { serve } from "https://deno.land/std@0.140.0/http/server.ts";

const TOKEN = "8160234854:AAFqXWBi6RpZ3CBXSqt9n7Sxb-vqV9C_4dM";
const API_URL = `https://api.telegram.org/bot${TOKEN}`;
const SPAM_KEYWORDS = ["airdrop", "bonus", "http", "https", "claim", "pump", "t.me", "binance"];

async function deleteMessage(chat_id: number, message_id: number) {
  await fetch(`${API_URL}/deleteMessage`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ chat_id, message_id }),
  });
}

async function handleUpdate(update: any) {
  if (!update.message || !update.message.text) return;

  const chat_id = update.message.chat.id;
  const message_id = update.message.message_id;
  const text = update.message.text.toLowerCase();

  if (SPAM_KEYWORDS.some(k => text.includes(k))) {
    await deleteMessage(chat_id, message_id);
    console.log("Spam deleted:", text);
  }
}

serve(async (req: Request) => {
  if (req.method === "POST") {
    const update = await req.json();
    await handleUpdate(update);
  }
  return new Response("Bot aktif!", { status: 200 });
});
