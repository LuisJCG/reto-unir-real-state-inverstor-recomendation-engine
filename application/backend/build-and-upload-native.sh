#!/bin/bash
# ./mvnw package -Pnative -Dquarkus.native.container-build=true -Dquarkus.container-image.build=true
PACKAGE=ghcr.io/jportoc/reto-unir-dataset:backend
VERSION=1.0.0
docker build  -f src/main/docker/Dockerfile.native -t "$PACKAGE-$VERSION" .
docker push "$PACKAGE-$VERSION"
