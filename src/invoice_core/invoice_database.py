import functools



class InvoiceDatabase:

@functools.cache
def __get_INVOICE_DB() -> InvoiceDatabase:
    return InvoiceDatabase(**Settings)