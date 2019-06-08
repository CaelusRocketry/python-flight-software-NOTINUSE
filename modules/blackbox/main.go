package blackbox

import (
    "encoding/csv"
    "os"
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

func save(in []string) {
    col := in
    if err := addcol("blackbox.csv", col); err != nil {
        panic(err)
    }
}
