#[path = "modules/_mod.rs"]
mod modules;

fn main() {
    println!("Hello from main()");
    modules::sensors::imu::imu_test();
}
