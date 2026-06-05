FROM thoom/pyresttest
COPY ./tests /usr/src/app
WORKDIR /usr/src/app
ENTRYPOINT [ "pyresttest" ]
EXPOSE 8081
CMD [ "https://e94zsuwqm3.execute-api.us-east-2.amazonaws.com","api_test.yml" ]