#[path = "modules/_mod.rs"]
mod modules;

use std::thread;
use std::time::Duration;

fn main() {
    println!("Hello from main()");
    let mut imu = modules::sensors::imu::IMU::init(0x28);

    let delay = Duration::from_millis(100);

    loop {
        let acc = imu.acc();
        println!("{:+2.2}\t{:+2.2}\t{:+2.2}", acc.0, acc.1, acc.2);
        thread::sleep(delay);
    }
}
