#!/bin/bash
# cmd bash time_and_run.sh -f path/to/yourfile.go

filename=""

while getopts ":f:" opt; do
  case $opt in
    f)
      filename=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$filename" ]; then
  echo "Usage: $0 -f filename"
  exit 1
fi

if [ ! -f "$filename" ]; then
  echo "File not found: $filename"
  exit 1
fi

case "${filename##*.}" in
  py)
    echo "Running Python file: $filename"
    time python "$filename"
    ;;
  go)
    echo "Building Go file: $filename"
    go build "$filename"
    if [ $? -eq 0 ]; then
      echo "Running Go file: $filename"
      time "./${filename%.go}"
    else
      echo "Build failed for $filename"
      exit 1
    fi
    ;;
  *)
    echo "Unsupported file type"
    exit 1
    ;;
esac