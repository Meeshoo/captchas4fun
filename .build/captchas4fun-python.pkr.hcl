source "docker" "python" {
  image = "python"
  commit = true
  changes = [
    "ENV FOO bar",
    "WORKDIR /captchas4fun",
    "CMD [\"captchas4fun.wsgi:application\", \"--bind\", \"0.0.0.0:80\"]",
    "ENTRYPOINT [\"gunicorn\"]"
  ]
}

build {
  sources = ["source.docker.python"]

  provisioner "shell" {
    inline = ["mkdir /captchas4fun"]
  }

  provisioner "file" {
    source = "../"
    destination = "/captchas4fun"
  }

  provisioner "shell" {
    inline = ["pip install -r /captchas4fun/requirements.txt"]
  }

  post-processors {
    post-processor "docker-tag" {
      repository = "550661752655.dkr.ecr.eu-west-1.amazonaws.com/captchas4fun-python"
      tags       = ["latest"]
    }

    post-processor "docker-push" {
      ecr_login = true
      login_server = "https://550661752655.dkr.ecr.eu-west-1.amazonaws.com/mitlan"
    }
  }
}
