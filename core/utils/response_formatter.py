
class ResponseFormatter:

    @staticmethod
    def run(response):
        rtn = {}
        if response is not None:
            rtn['data'] = response
        return rtn
