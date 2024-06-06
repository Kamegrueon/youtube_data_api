output "pubsub_topic_id" {
  value = google_pubsub_topic.main.id
}

output "pubsub_topic_name" {
  value = google_pubsub_topic.main.name
}

output "pubsub_topic_dead_letter_id" {
  value = google_pubsub_topic.main_dead_letter.id
}
