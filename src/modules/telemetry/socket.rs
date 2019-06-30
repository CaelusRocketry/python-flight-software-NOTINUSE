extern crate ws;

use std::thread;
use std::thread::sleep;
use std::time::Duration;

use ws::{connect, listen, CloseCode, Handler, Message, Result, Sender, Handshake};
use chrono::prelude::*;

use crate::modules::telemetry::logging::*;

// Server WebSocket handler
struct Server {
    out: Sender,
}

impl Handler for Server {
    fn on_open(&mut self, shake: Handshake) -> Result<()> {
        // Log that telemetry connection opened
        let open_log = Log {
            message: String::from("Open websocket connection"),
            timestamp: Utc::now(),
            sender: String::from("TELEM.SERVER"),
            level: Level::Info
        };

        self.out.send(format!("{}", open_log));

        Ok(())
    }

    fn on_message(&mut self, msg: Message) -> Result<()> {
        // TODO: Ingest and execute messages instead of printed them
        println!("RECV: '{}'", msg);

        Ok(())
    }

    fn on_close(&mut self, code: CloseCode, reason: &str) {
        println!("WebSocket closing for ({:?}) {}", code, reason);
        println!("Shutting down server after first connection closes.");
        self.out.shutdown().unwrap();
    }
}

pub fn start() {
    // Server thread
    let server =
        thread::spawn(move || listen("192.168.1.70:3012", |out| Server { out: out }).unwrap());
}
