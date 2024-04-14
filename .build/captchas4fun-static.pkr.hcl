source "docker" "base_captchas4fun" {
  image = "550661752655.dkr.ecr.eu-west-1.amazonaws.com/base-captchas4fun"
  commit = true
  ecr_login = true
  aws_access_key = var.access_key
  aws_secret_key = var.secret_key
  login_server = "https://550661752655.dkr.ecr.eu-west-1.amazonaws.com/mitlan"
  changes = [
    "ENV FOO bar",
    "ENTRYPOINT [\"nginx\", \"-g\", \"daemon off;\"]"
  ]
}

build {
  sources = ["source.docker.base_captchas4fun"]

  provisioner "shell" {
    inline = ["mkdir /captchas4fun"]
  }

  provisioner "file" {
    source = "../static"
    destination = "/captchas4fun"
  }

  post-processors {
    post-processor "docker-tag" {
      repository = "550661752655.dkr.ecr.eu-west-1.amazonaws.com/captchas4fun-static"
      tags       = ["latest"]
    }

    post-processor "docker-push" {
      ecr_login = true
      login_server = "https://550661752655.dkr.ecr.eu-west-1.amazonaws.com/mitlan"
    }
  }
}
