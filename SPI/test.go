package main

import "fmt"

func main() {

  dict := make(map[string]func(x int) int)

  dict["test"] = test

  fmt.Println(dict["test"](2))
  // printSlice(s)
}

func test(y int) int {
  return y + 1
}
