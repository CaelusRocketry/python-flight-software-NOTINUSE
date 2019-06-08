package blackbox

import (
    "encoding/csv"
    "os"
    "time"
    "strconv"
)

func addcol(fname string, column []string) error {
    // read the file
    f, err := os.Open(fname)
    if err != nil {
        return err
    }
    r := csv.NewReader(f)
    lines, err := r.ReadAll()
    if err != nil {
        return err
    }
    if err = f.Close(); err != nil {
        return err
    }

    // add column
    l := len(lines)
    if len(column) < l {
        l = len(column)
    }
    for i := 0; i < l; i++ {
        lines[i] = append(lines[i], column[i])
    }

    // write the file
    f, err = os.Create(fname)
    if err != nil {
        return err
    }
    w := csv.NewWriter(f)
    if err = w.WriteAll(lines); err != nil {
        f.Close()
        return err
    }
    return f.Close()
}

func save(t time.Time, d []float64) {
    text := []string{}
    text = append(text, t.String())
    for i := range d {
        n := values[i]
        line := strconv.FormatFloat(input_num, 'f', 6, 64)
        text = append(text, line)
    }
    if err := addcol("blackbox.csv", text); err != nil {
        panic(err)
    }
}
