from scrapy.http import Request, HtmlResponse


def fake_response_from_file(file_name) -> HtmlResponse:
    url = "https://example.com"
    request = Request(url=url)

    with open(file_name, "r") as f:
        file_content = f.read()
        response = HtmlResponse(url=url,
                                request=request,
                                body=file_content,
                                encoding="utf-8")

        return response
