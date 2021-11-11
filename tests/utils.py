import vcr as base_vcr

vcr = base_vcr.VCR(
    path_transformer=base_vcr.VCR.ensure_suffix(".yaml"),
    ignore_hosts=("test",),
    cassette_library_dir="tests/fixtures/vcr",
)
