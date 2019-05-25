package sensors

// Levels type
type Levels string

// constants for the levels of danger when returning sensor checks
const (
	SAFE     Levels = 0
	WARNING  Levels = 1
	CRITICAL Levels = 2
)
