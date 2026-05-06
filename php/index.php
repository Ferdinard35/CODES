<?php
require_once 'GenericBook.php';
$book = new GenericBook(400, 600);
echo "page count:" . $book->getPageCount() . "\n";
$book1 = new GenericBook();
echo "page count:" . $book1->getPageCount() . "\n";
