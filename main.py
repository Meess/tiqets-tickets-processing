""" 
Executing the tiqets assignment, described in:
Tiqets Programming Assignment - CSV files.pdf
"""

import read
import sys
import printer
from transformer import Table, Orders, Barcodes

if __name__ == '__main__':
    """
    Arguments:
        output_path   : file path for output
        barcodes_path : path to barcodes.csv
        orders_path   : path to orders.csv
    """

    # Get the file path for the output
    output_path   = sys.argv[1]
    output_file   = open(output_path, 'w+')

    # Get data paths
    barcodes_path = sys.argv[2]
    orders_path   = sys.argv[3]

    # Read barcode and order data into a Tables
    barcodes = Table.make_table_from_path(barcodes_path, read.csv)
    orders   = Table.make_table_from_path(orders_path  , read.csv)

    duplicate_barcodes = barcodes.duplicate('barcode', return_class=Barcodes)
    unused_barcodes    = barcodes.without('order_id')
    valid_barcodes     = barcodes.remove(unused_barcodes, duplicate_barcodes)

    # Link orders and barcodes
    orders_with_barcode = orders.merge(valid_barcodes,
                                       on="order_id", 
                                       return_class=Orders)

    most_ordering_customers = orders_with_barcode.most_frequent('customer_id',
                                                                'barcode',
                                                                top=5)

    # Print assignment results
    printer.print_valid_orders(orders_with_barcode, output_file)
    printer.print_empty_orders(orders_with_barcode.without('barcode'),
                               sys.stderr)
    printer.print_duplicate_barcodes(duplicate_barcodes, sys.stderr)
    printer.print_unused_barcodes(unused_barcodes, sys.stderr)
    printer.print_most_ordering_customers(most_ordering_customers, sys.stdout)

    output_file.close()