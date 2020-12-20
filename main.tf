provider "aws" {
    region = var.AWS_REGION
}

resource "aws_sqs_queue" "my_dead_letter_queue" {
    name = "my_dead_letter_queue-${terraform.workspace}"
}

resource "aws_sqs_queue" "terraform_queue_principal" {
    
    name = "terraform-fila-principal-${terraform.workspace}"
    delay_seconds = 90
    max_message_size = 2048
    message_retention_seconds = 86400
    receive_wait_time_seconds = 10
    redrive_policy = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.my_dead_letter_queue.arn}\",\"maxReceiveCount\":1}"

}

resource "aws_sqs_queue" "terraform_queue_secundario" {
    name = "terraform-fila-secundaria-${terraform.workspace}"
    delay_seconds = 90
    max_message_size = 2048
    message_retention_seconds = 86400
    receive_wait_time_seconds = 10
}

resource "aws_cloudformation_stack" "tf_sns_topic" {
   name = "snsStack"
   template_body = data.template_file.aws_cf_sns_stack.rendered
   tags = {
     name = "snsStack"
   }
 }
 
data "template_file" "aws_cf_sns_stack" {
   template = file("${path.module}/templates/cf_aws_sns_email_stack.json.tpl")
   vars = {
     sns_topic_name        = "sns-topic-${terraform.workspace}"
     sns_display_name      = "Topico_Messagens"
     sns_subscription_list = join(",", formatlist("{\"Endpoint\": \"%s\",\"Protocol\": \"%s\"}",
     "valteircardoso@yahoo.com.br",
     "email"))
   }
 }
