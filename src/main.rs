#[path = "modules/_mod.rs"]
mod modules;

use std::thread;
use std::time::Duration;

use crate::modules::sensors::imu::IMU;
use crate::modules::sensors::pressure::Pressure;
use crate::modules::sensors::SensorTrait;

fn main() {
    let mut imu = IMU::new("NOSECONE", 0x28);
    let mut pressure = Pressure::new("TANK");

    let delay = Duration::from_millis(200);

    println!("Sensor registered: {}", pressure.name());
    println!("Sensor registered: {}", imu.name());

    loop {
        imu.status();
        thread::sleep(delay);
    }
}

// fn main() {
//     modules::telemetry::telem::runsocket();
// }
