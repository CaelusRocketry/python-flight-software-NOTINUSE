extern crate chrono;

use std::fmt;

use chrono::prelude::*;

#[derive(Hash, Debug)]
pub enum Level {
    Info,
    Warn,
    Crit,
    Debug
} 

#[derive(Hash)]
pub struct Log {
    message: String,
    timestamp: DateTime<Utc>,
    sender: String,
    level: Level
}

// Allows us to use to_string() to display the Log in a readable format
impl fmt::Display for Log {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} [{:?}] {}: {}", self.timestamp, self.level, self.sender, self.message)
    }
}

// Using `derive` doesn't work with Log, so we have to implement it manually
impl PartialEq for Log {
    fn eq(&self, other: &Self) -> bool {
        self.to_string() == other.to_string()
    }
}
impl Eq for Log {}
