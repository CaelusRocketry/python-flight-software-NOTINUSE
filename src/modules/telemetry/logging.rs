use std::time::SystemTime;

#[derive(Hash)]
pub enum Level {
    Info,
    Warn,
    Crit,
    Debug
} 

#[derive(Hash)]
pub struct Log {
    message: String,
    timestamp: SystemTime,
    sender: String,
    level: Level
}

// Using `derive` doesn't work with Log, so we have to implement it manually
impl PartialEq for Log {
    fn eq(&self, other: &Self) -> bool {
        self.message == other.message
    }
}
impl Eq for Log {}
