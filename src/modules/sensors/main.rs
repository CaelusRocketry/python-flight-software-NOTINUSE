pub struct Sensor {
    pub name: str,
    pub safe_val: i16,
    pub warn_val: i16,
    pub crit_val: i16
}

trait Sensor {
    pub fn value(&self) -> i16;
    pub fn correct(&self) -> bool;
}