#!/bin/bash
USER="postgres"
DATABASE="installers"
HOST="localhost"
BACKUP_DIRECTORY="/home/romak/pg_backup"


CURRENT_DATE=$(date "+%Y%m%d")

#pg_dump -U "$USER" -h "$HOST" "$DATABASE" | gzip - > "$BACKUP_DIRECTORY/$DATABASE_$CURRENT_DATE.sql.gz"
BACKUP_FILE="$BACKUP_DIRECTORY/$DATABASE_$CURRENT_DATE.bak"

pg_dump -U "$USER" -h "$HOST" -F c -b -f "$BACKUP_FILE" "$DATABASE"

gzip "$BACKUP_FILE"

# Cleanup backups older than 7 days
find "$BACKUP_DIRECTORY" -name "*.bak.gz" -mtime +7 -exec rm {} \;
echo "Done."