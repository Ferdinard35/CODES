<?php
class GenericBook
{
    private $pageCount;
    private $price;
    // Constructor
    public function __construct($pageCount = 0, $price = 0)
    {
        $this->pageCount = $pageCount;
        $this->price = $price;
    }
    public function getPageCount()
    {
        return $this->pageCount;
    }
    public function getPrice()
    {
        return $this->price;
    }
    public function setprice($price)
    {
        $this->price = $price;
    }
    public function setPageCount($pageCount)
    {
        $this->pageCount = $pageCount;
    }
    public function getype()
    {
        return "Generic Book";
    }
}
