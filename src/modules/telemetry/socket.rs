extern crate ws;

use std::thread;
use std::thread::sleep;
use std::time::Duration;

use ws::{connect, listen, CloseCode, Sender, Handler, Message, Result};

// Server WebSocket handler
struct Server {
    out: Sender,
}

impl Handler for Server {
    fn on_message(&mut self, msg: Message) -> Result<()> {
        println!("RECV: '{}'. ", msg);
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
