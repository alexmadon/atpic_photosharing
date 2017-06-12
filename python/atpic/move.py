"""
move a gallery within another gallery

move a pic into another gallery

need to shows <select><option>

need to actually do the move in SQL and filesystem


URLs:
GET /gallery/1/move/gallery
GET /gallery/1/move/gallery?page=2

GET /gallery/1/move
GET /gallery/1/move?page=2

loop at the same level: (need to rename 'dir' as 'gallery' in model)
GOOD:
GET /gallery/1/gallery
GET /gallery/1/gallery?page=2
PUT /gallery/1/gallery/3
POST /gallery/1/gallery/3/put

GET /gallery/1/togallery
GET /gallery/1/togallery?page=2

BAD url schema as it breask the object/ID rule:

GET /gallery/1/pic/99/move/gallery
GET /gallery/1/pic/99/move/gallery?page=2
PUT /gallery/1/pic/99/move/gallery/3
POST /gallery/1/pic/99/move/gallery/3/put


GOOD:
GET /gallery/1/pic/99/gallery
GET /gallery/1/pic/99/gallery?page=2
PUT /gallery/1/pic/99/gallery/3
POST /gallery/1/pic/99/gallery/3/put




GET /selection
GET /selection/actions
GET /selection/delete
DELETE /selection
GET /selection/tag
GET /selection/tocart
GET /selection/togallery
GET /selection/move/cart
PUT /selection/cart
GET /selection/move/gallery
PUT /selection/gallery/3



cf PHP:

forge_query_gallery_of_artist
check_notanancestor




//==================================================
function check_notanancestor($gallery2test,$galleryid,$artistid,$socket){
    //this is to avoid loops: A->B->A
    //this take a $gallery2test
    //check its "dir" recursively to see if we find $galleryid
    //in its parent
    //returns TRUE if we find no parent

    //print "check_notanancestor($gallery2test,$galleryid,$artistid,$socket)<br/>\n";
    if (!$gallery2test){
        //print "GOOD: $gallery2test is the root directory /<br/>\n";
        return TRUE;//GOOD: $gallery2test is the root directory /
    }


    $query=forge_query_gallery_check_gallery_not_ancestor($gallery2test,$galleryid,$artistid);


    $result=send_query_select($query,$socket);
    $num_rows = $result->rows;
    if ($num_rows){
        list(,$row)=each($result->data);
        $dir=$row["dir"];
        if ($dir==$galleryid){
            //print "BAD: $gallery2test is an ancestor of $galleryid!!!<br/>\n";
            return FALSE;//BAD: $gallery2test is an ancestor of $galleryid!!!
        } else {
            if (!$dir){
                //print "GOOD: we hit the root directory /<br/>\n";
                return TRUE;//GOOD: we hit the root directory /
            } else{
                //recurse
                //print "recurse<br/>";
		return check_notanancestor($dir,$galleryid,$artistid,$socket);
            }
        }
    } else {
        //print "BAD: this hould not happen<br/>\n";
        return FALSE;//BAD: this hould not happen
    }
}





function forge_query_gallery_check_gallery_not_ancestor($gallery2test,$galleryid,$artistid){
    $query="select * 
from artist_gallery
where 
id='$gallery2test'
and refartist='$artistid'";
    return $query;
}


"""
