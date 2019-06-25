#[path = "modules/_mod.rs"]
mod modules;

use std::thread;
use std::time::Duration;

use crate::modules::sensors::imu::IMU;
use crate::modules::sensors::pressure::Pressure;
use crate::modules::sensors::SensorTrait;

fn main() {
    let mut imu = IMU::new("NOSECONE", 0x28);
    let mut pressure_tank = Pressure::new("TANK", 1.75, 2.0);

    let delay = Duration::from_millis(200);

    println!("Sensor registered: {}", pressure_tank.name());
    println!("Sensor registered: {}", imu.name());

    loop {
        println!("{:?}", pressure_tank.status());
        thread::sleep(delay);
    }
}

// fn main() {
//     modules::telemetry::telem::runsocket();
// }
