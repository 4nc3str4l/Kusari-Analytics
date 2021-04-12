package main

import (
	"github.com/streadway/amqp"
	"log"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func SetupRabbitMQ(chBlockNumber chan []byte, chTransactions chan []byte, closing chan bool) {
	// Try to connect from outside
	conn, err := amqp.Dial("amqp://user:password@localhost:5672/")

	// If we fail we can try to connect to the rabbit mq inside the docker
	if err != nil {
		conn, err = amqp.Dial("amqp://user:password@rabbit:5672/")
		failOnError(err, "Failed to connect to RabbitMQ")
	}

	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	go subscribeToQueue(ch, "kusari", chBlockNumber)
	go subscribeToQueue(ch, "transactions", chTransactions)

	<-closing
}

func subscribeToQueue(rbChan *amqp.Channel, name string, receiver chan[] byte) {
	q, err := rbChan.QueueDeclare(
		name,
		false,
		false,
		false,
		false,
		nil,
	)

	failOnError(err, "Failed to declare queue")

	for {
		messages, err := rbChan.Consume(
			q.Name,
			"",
			true,
			false,
			false,
			false,
			nil,
		)
		failOnError(err, "Failed to register a consumer")

		for d := range messages {
			receiver <- d.Body
		}
	}
}
