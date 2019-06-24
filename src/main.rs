#[path = "modules/_mod.rs"]
mod modules;

use std::thread;
use std::time::Duration;

use crate::modules::sensors::SensorTrait;

fn main() {
    let mut imu = modules::sensors::imu::IMU::new("NOSECONE", 0x28);

    let delay = Duration::from_millis(200);

    println!("{}:", imu.name());

    loop {
        imu.status();
        thread::sleep(delay);
    }
}

// fn main() {
//     modules::telemetry::telem::runsocket();
// }
