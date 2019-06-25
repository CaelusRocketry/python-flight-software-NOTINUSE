#[path = "modules/_mod.rs"]
mod modules;

use modules::supervisor::main as supervisor;

fn main() {
    supervisor::start();
}
