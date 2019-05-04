package sensors

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

// only needed below for sample processing

func TestServer() {

	fmt.Println("Launching server...")

	// listen on all interfaces
	ln, _ := net.Listen("tcp", "192.168.1.84:8081")

	fmt.Println("Listening")

	// accept connection on port
	conn, _ := ln.Accept()

	fmt.Println("Connected")

	// run loop forever (or until ctrl-c)
	for {
		// will listen for message to process ending in newline (\n)
		message, _ := bufio.NewReader(conn).ReadString('\n')
		// output message received
		fmt.Print("Message Received:", string(message))
		// sample process for string received
		newmessage := strings.ToUpper(message)
		// send new string back to client
		conn.Write([]byte(newmessage + "\n"))
	}
}

func TestClient() {

	// connect to this socket
	fmt.Println("Cool stuff")
	conn, _ := net.Dial("tcp", "127.0.0.1:8081")
	fmt.Println("Cooler stuff")
	for i := 0; i < 10; i++ {
		// read in input from stdin
		fmt.Println("Client hello")
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Text to send: ")
		text, _ := reader.ReadString('\n')
		// send to socket
		fmt.Fprintf(conn, text+"\n")
		// listen for reply
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Print("Message from server: " + message)
	}
}
