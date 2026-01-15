FROM ruby:4.0-slim

WORKDIR /app


RUN apt-get update && \
    apt install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY /portfolio-site/Gemfile* /app/

RUN gem install bundler && \
    bundle install && \
    apt purge -y --auto-remove build-essential

COPY /portfolio-site /app

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
