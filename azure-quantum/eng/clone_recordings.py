"""
Copy the sync recordings to the aio recordings

Run from the azure-quantum directory.
"""

import pathlib
import yaml


def main():
    recordings_sync = pathlib.Path('tests/unit/recordings')
    recordings_async = pathlib.Path('tests/unit/aio/recordings')
    assert recordings_sync.exists() and recordings_async.exists()
    for recording in recordings_sync.glob('*.yaml'):
        with open(recording) as rec:
            recording_data = yaml.safe_load(rec)
            assert 'interactions' in recording_data
            for interaction in recording_data['interactions']:
                interaction['response']['url'] = interaction['request']['uri']

            with open(recordings_async / recording.name, 'x') as async_recording:
                yaml.safe_dump(recording_data, async_recording)

if __name__ == "__main__":
    main()