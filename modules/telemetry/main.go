package telemetry

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"time"
)

// only needed below for sample processing
var IP = "192.168.1.180:8081"
var QUEUE []string

func TestServer() {

	fmt.Println("Launching server...")

	// listen on all interfaces
	ln, _ := net.Listen("tcp", IP)

	fmt.Println("Listening")

	// accept connection on port
	conn, _ := ln.Accept()

	fmt.Println("Connected")

	//	go sendStuff(true, conn)
	go listenStuff(conn)
	for {

	}
}

func listenStuff(conn net.Conn) {
	fmt.Println("Doing stuff")
	for {
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Println("Message Received:", string(message))
		var pack Packet
		json.Unmarshal([]byte(message), &pack)
		message = Ingest(pack)
		if message == "ABORT" {
			fmt.Println("ABORTING NOW, GLHF")
			return
		}
	}
}

func sendStuff(isServer bool, conn net.Conn) {
	for {
		if len(QUEUE) > 0 {
			msg := QUEUE[0]
			if isServer {
				conn.Write([]byte(msg + "\n"))
			} else {
				fmt.Fprintf(conn, msg+"\n")
			}
			QUEUE = QUEUE[1:]
		}
	}
}

func TestClient() {

	// connect to this socket
	conn, _ := net.Dial("tcp", IP)
	fmt.Println("Client connected")

	go sendStuff(false, conn)
	//	go listenStuff(conn)

	for i := 0; i < 5; i++ {
		Enqueue("abc", "Temp")
		time.Sleep(500 * time.Millisecond)
		Enqueue("abc", "Pressure")
		time.Sleep(500 * time.Millisecond)
	}
	Enqueue("abc", "ABORT")
	for i := 0; i < 5; i++ {
		Enqueue("abc", "Temp")
		time.Sleep(500 * time.Millisecond)
		Enqueue("abc", "Pressure")
		time.Sleep(500 * time.Millisecond)
	}
	//	for {
	//		reader := bufio.NewReader(os.Stdin)
	//		fmt.Print("Text to send: ")
	//		text, _ := reader.ReadString('\n')
	// send to socket

	//		fmt.Fprintf(conn, text+"\n")
	// listen for reply
	//		message, _ := bufio.NewReader(conn).ReadString('\n')
	//		fmt.Print("Message from server: " + message)
	//	}
}

func Listen() {
	fmt.Println("Hey testing Listen")
}

func Send() {
	fmt.Println("hey testing send")
}

/*
corresponding code in Python:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.84', 8081))

*/
