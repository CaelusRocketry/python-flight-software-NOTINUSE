extern crate chrono;

use chrono::prelude::*;
use std::fmt;

use crate::modules::sensors::SensorStatus;

#[derive(Hash, Debug)]
pub enum Level {
    Info,
    Debug,
    Warn,
    Crit,
}

impl Level {
    pub fn sensor_status_to_level(status: &SensorStatus) -> Level {
        match status {
            SensorStatus::Safe => Level::Info,
            SensorStatus::Warn => Level::Warn,
            SensorStatus::Crit => Level::Crit,
        }
    }
}

impl fmt::Display for Level {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Level::Info => write!(f, "INFO"),
            Level::Debug => write!(f, "DBUG"),
            Level::Warn => write!(f, "WARN"),
            Level::Crit => write!(f, "CRIT"),
        }
    }
}

#[derive(Hash)]
pub struct Log {
    pub message: String,
    pub timestamp: DateTime<Utc>,
    pub sender: String,
    pub level: Level,
}

// Allows us to use to_string() to display the Log in a readable format
impl fmt::Display for Log {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "[{}] [{}] [{}] {}",
            self.timestamp.format("%+"),
            self.level,
            format!("{: ^16}", self.sender),
            self.message
        )
    }
}

// Using `derive` doesn't work with Log, so we have to implement it manually
impl PartialEq for Log {
    fn eq(&self, other: &Self) -> bool {
        self.to_string() == other.to_string()
    }
}
impl Eq for Log {}
