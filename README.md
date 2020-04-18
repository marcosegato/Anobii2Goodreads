# Anobii2Goodreads

This script converts a standard CSV export from the Anobii website to a format you should be able to import into Goodreads.

- Anobii homepage: [https://anobii.com](https://anobii.com)
- Goodreads homepage: [https://goodreads.com](https://goodreads.com)

# How to export from Anobii and import to Goodreads

## Prerequisites

Python v2.7.x installed

## Export from Anobii

1. Login to Anobii and access your books library page
2. Click on the option button you can find on the top right, besides ordering filters
3. Select "Export list" option and select CSV format 
4. You will receive an email in a few minutes with a CSV file attached. Download this file and rename it as `anobii_export.csv`.

## Convert from Anobii to Goodreads

1. To convert between the export format of Anobii and import format of Goodreads, we use the [Anobii2Goodreads](https://github.com/marcosegato/Anobii2Goodreads) script. Git clone it or download the code:
    ```shell
    $ git clone https://github.com/marcosegato/Anobii2Goodreads
    ```
2. Place the `anobii_export.csv` file in the same directory containing the `anobii-to-goodreads.py` script.
3. Perform the conversion, the output is written to `import_to_goodreads.csv` file:
    ```shell
    $ python anobii-to-goodreads.py
    ```
## Import to Goodreads

1. Login to Goodreads. Go to its [import page](https://goodreads.com/review/import/) and import the `import_to_goodreads.csv` file.
2. Refresh this page to see the import progress. Few books may not be imported (e.g. missing ISBN), consider [adding them manually](https://www.goodreads.com/book/new).
3. Go to your own update stream, you should be able to see all the imports. Do not worry, Goodreads only shows a few of these updates on your friends' stream.

# Credits

This script is based on the following works:

* Original version by Giacomo Lacava published on 2008: 
[http://blog.pythonaro.com/2008/08/export-your-books-from-anobii-to_14.html](http://blog.pythonaro.com/2008/08/export-your-books-from-anobii-to_14.html)
* Improvements by Tijs Teulings to make it work again with the latest expot format on 2015: [https://codeyarns.com/2015/07/03/how-to-export-from-anobii-and-import-to-goodreads/](https://codeyarns.com/2015/07/03/how-to-export-from-anobii-and-import-to-goodreads/)

# License
GNU General Public License version 3