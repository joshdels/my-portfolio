#!/usr/bin/env bash

set -Eeuo pipefail

: "${PORTFOLIO_IMAGE:?PORTFOLIO_IMAGE must contain the immutable image reference}"
: "${GHCR_USER:?GHCR_USER is required}"
: "${GHCR_TOKEN:?GHCR_TOKEN is required}"

compose_file=".docker/docker-compose.yml"
if docker compose version >/dev/null 2>&1; then
  compose=(docker compose -f "$compose_file")
elif command -v docker-compose >/dev/null 2>&1; then
  compose=(docker-compose -f "$compose_file")
else
  echo "Docker Compose is not installed." >&2
  exit 1
fi

previous_image="$(docker inspect --format '{{.Config.Image}}' my-portfolio 2>/dev/null || true)"
rollout_started=false

cleanup() {
  local status=$?
  trap - EXIT

  if [ "$status" -ne 0 ] && [ "$rollout_started" = true ] && [ -n "$previous_image" ]; then
    echo "Deployment failed; restoring the previous application image."
    export PORTFOLIO_IMAGE="$previous_image"
    "${compose[@]}" up -d --no-build --remove-orphans || true
  fi

  "${compose[@]}" rm -f 2>/dev/null || true
  docker image prune -f || true
  docker logout ghcr.io >/dev/null 2>&1 || true
  exit "$status"
}
trap cleanup EXIT

printf '%s' "$GHCR_TOKEN" | docker login ghcr.io --username "$GHCR_USER" --password-stdin
docker pull "$PORTFOLIO_IMAGE"

echo "Running production checks with the tested image."
"${compose[@]}" run --rm --no-deps web python manage.py check --deploy --fail-level ERROR

echo "Applying existing database migrations."
"${compose[@]}" run --rm --no-deps web python manage.py migrate --noinput

rollout_started=true
"${compose[@]}" up -d --no-build --remove-orphans

health="unknown"
for attempt in $(seq 1 36); do
  health="$(docker inspect --format '{{.State.Health.Status}}' my-portfolio 2>/dev/null || true)"
  if [ "$health" = "healthy" ]; then
    break
  fi
  if [ "$health" = "unhealthy" ]; then
    "${compose[@]}" logs --tail=150 web
    exit 1
  fi
  sleep 5
done

if [ "$health" != "healthy" ]; then
  "${compose[@]}" logs --tail=150 web
  exit 1
fi

echo "Deployment complete: $PORTFOLIO_IMAGE"
