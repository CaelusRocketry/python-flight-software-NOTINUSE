#[path = "modules/_mod.rs"]
mod modules;

use std::thread;
use std::time::Duration;

fn main() {
    println!("Hello from main()");
    let imu = modules::sensors::imu::IMU::init(0x28);

    let delay = Duration::from_millis(100);

    loop {
        let accel = imu.acc();
        println!("{:+2.2}\t{:+2.2}\t{:+2.2}", accel.0, accel.1, accel.2);
        thread::sleep(delay);
    }
}
