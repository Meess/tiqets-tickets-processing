"""
This file contains functions and classes for printing datasets into
the right format.
"""

def print_valid_orders(table, file):
    for record in table:
        barcodes = [int(barcode) for barcode in record.barcode]
        template = "{},{},{}"
        print(template.format(record.customer_id, 
                              record.order_id, 
                              barcodes), file=file)

def print_duplicate_barcodes(table, file):
    for record in table:
        template = "ERROR: Duplicate barcode: {}"
        print(template.format(record.barcode), file=file)

def print_empty_orders(table, file):
    for record in table:
        template = "ERROR: order {} has no associated barcode(s)"
        print(template.format(record.order_id[0]), file=file)

def print_unused_barcodes(table, file):
    for record in table:
        template = "ERROR: unused barcode {}"
        print(template.format(record.barcode[0]), file=file)

def print_most_ordering_customers(table, file, per_row=True):
    for record in table:
        template = "{},{}"
        print(template.format(record.customer_id[0],
                              record.barcode[0]), file=file)  
