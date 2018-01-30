EXAMPLE_MAP = [
    {
        "id" : "video",
        "maxWidth" : 960,
        "maxHeight" : 540,
        "maxFrameRate" : 25,
        "contentType" : "video",
        "segmentAlignment" : True,
        "bitstreamSwitching" : True,
        "representations" : [
            {
                "manifest_name" : "demo_high",
                "source_id" : "demo_high_H264",
                "target_id" : "video_high",
            },
            {
                "manifest_name" : "demo_low",
                "source_id" : "demo_low_H264",
                "target_id" : "video_low"
            }
        ]
    },
    {
        "id" : "audio_en",
        "contentType" : "audio",
        "segmentAlignment" : True,
        "bitstreamSwitching" : True,
        "lang" : "en",
        "representations" : [
            {
                "manifest_name" : "demo_high",
                "source_id" : "demo_high_AAC",
                "target_id" : "audio_en",
            }
        ]
    },
    {
        "id" : "audio_it",
        "contentType" : "audio",
        "segmentAlignment" : "true",
        "bitstreamSwitching" : "true",
        "lang" : "it",
        "representations" : [
            {
                "manifest_name" : "demo_low",
                "source_id" : "demo_low_AAC",
                "target_id" : "audio_it",
            }
        ]
    },
]
