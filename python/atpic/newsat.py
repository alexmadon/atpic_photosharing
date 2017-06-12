def news_new():
    return """
    <news date="2008-05-26">
    <b>
    <t id="2040">New 'direct' server names scheme and 'direct' URLs:</t>
    </b>
     
    
    <t id="2041">As you may know Atpic uses a cluster of web servers to store and serve the pictures.</t>
     
    
    <t id="2042">This is good as it allows the web site to scale well with the number of members.</t>
     
    
    <t id="2043">But we had two problems with the server names:</t>
     
    
    <ul>
    <li>
    <i> 
    <t id="2056">Changing names of FTP servers.</t>
    </i> 
    




    <t id="2044">As a user may be moved from one server to another server the FTP server name was subject to change.</t>
     
    
    <t id="2045">Now, the FTP server name will remain the same for the acount life and is:</t>
     <i>uUID.direct.atpic.com</i>.
         

    <t id="2046">If for instance the account User ID (UID) is 999, then your direct server will be:</t>
     <i>u999.direct.atpic.com</i>.
     
    
    
     </li>
   
    <li>
    <i>
    <t id="2055">Performance issues in 'hot linking'.</t>
    </i>
     
    
    <t id="2047">This new server naming is also used for 'hot linking'.</t>
     

    <t id="2048">You do 'hot linking' when, for instance, you post a direct link to an Atpic picture from a forum.</t>
     
    <t id="2049">The old direct URLs were built as follows:</t>
    <div style="text-align:center">
    <i>http://direct.atpic.com/UID/GID/Secret/PID/Resolution.Extension</i>
     </div>

    <t id="2050">When a lot of users were posting images in forums using those URLs, the overhead generated by looking up on what server the picture actually was, was causing big performance issues.</t>
     
    <t id="2051">The new URL format is:</t>
     
    <div style="text-align:center">
    <i>http://uUID.direct.atpic.com/GID/Secret/PID/Resolution.Extension</i>
    </div>
    </li>
    </ul>

    <t id="2052">We hope this new convention will allow our infrastucture to serve fast the ever increasing amount of pictures hosted on Atpic.</t>
     
    
    <t id="2053">We apologize for the inconvenience caused by this change, but the decision had to be made for the future of Atpic.</t>
     
    
    <a href="http://faq.atpic.com">
    <t id="2054">More information is available in the FAQ.</t>
    </a> 


    </news>


    <news date="2008-02-19">
    <t id="594">The immersive gallery slideshow from Piclens is now available on Atpic.</t>
     
    
    <t id="595">Go to any gallery page with firefox and the piclens plugin, click on the Piclens slideshow link and navigate within the gallery in 3 dimensions!</t>
     
    
    <t id="596">Enjoy!</t>

     <div style="text-align:center; margin:auto;">
    <img src="news/200screen1.png" style="margin:5px;padding:5px;" alt="screen1"/>
    <img src="news/200screen2.png" style="margin:5px;padding:5px;" alt="screen2"/>
    <img src="news/200screen3.png" style="margin:5px;padding:5px;" alt="screen3"/>
    
     </div>

    </news>


    <news date="2008-01-06">
    <t id="854">A simple PM (Private Message) system has been released.</t>
     
    <t id="855">On the contrary to Atpic Comments, a Private Message will not be shown on the web site.</t>
     
    <t id="856">Non Atpic members are able to send a member a PM but will have to leave a valid email address to be contacted back.</t>
     
    <t id="857">Atpic members can contact other Atpic members using a PM and their email will not be shown to the recipient of the message.</t>
     
    <t id="858">Atpic administrators will also use the messaging system to contact the members.</t>
     
    <t id="859">Indeed we have been answering support questions asked by Atpic users and the answer mail has never been received.</t>
     
    <t id="860">This is the case of many users having an email address at hotmail.com.</t>
     
    <t id="861">It seems the hotmail.com anti-spam software blocks many valid mails.</t>
     
    <t id="862">The system look and feel will be improved over time.</t>
     
    <t id="863">As for comments, an email notification will be sent to the message recipient each time a new PM is created.</t>
     
    <t id="864">You can read your Private Messages once logged into your account by clicking on the 'pm' link.</t>
     
     </news>


    <news date="2008-01-01">
    <t id="850">A new slide show written in Flash is now available.</t>
     
    <t id="851">This is an easy way to include your pictures in other web sites.</t>
     
    <t id="852">It is aslo a nice nd interactive way of presenting your photos.</t>
     
    <a href="http://faq.atpic.com/$setlang#slideshowflash">
    <t id="853">More details can be found in the wiki.</t>
    </a> 
    </news>


    <news date="2007-10-20">
    <t id="845">Unfortunately, due to performance issues, we had to change the way Atpic documents are hotlinked.</t>
     
    <t id="846">The simpler but less efficient scheme based on the 'raw' URLs has now been replaced by a more involved but much more efficient scheme.</t>
     
    <t id="847">The new scheme based on a new hostname 'direct.atpic.com' is described in the FAQ and direct URLs are displayed on each document presentation page for easy cut and paste.</t>
     
    </news>





    <news date="2007-09-10">
    <b><t id="389">Yet another cool Atpic feature:</t></b>
     
    <t id="390">How many times a day do you visit Google home page?</t>
     
    <t id="391">Wouldn't it be cool to view one of your pictures each time you visit google.com?</t>
     
    <t id="392">Well, at Atpic, we thought it would and we created</t>
     <b><a href="http://google.atpic.com">google.atpic.com</a></b>. 

    <t id="393">Each time you visit this page you will see in background a picture hosted on Atpic.com.</t>
     
    <t id="394">You can choose between a random Atpic picture, a random picture made by an Atpic member (you for instance), a random picture within a gallery, or a predefined picture.</t>
     
    <t id="395">The result of your google search will also have the picture as background.</t>
     
    <a href="http://faq.atpic.com/$setlang#google">
    <t id="396">More information is available in the FAQ.</t>
    </a> 
    <t id="397">Come to Atpic's blog to discuss this new coolest feature!</t>
     
    </news>




    <news date="2007-09-08">
    <t id="385">Atpic has now its blog:</t>
     <a href="http://blog.atpic.com">blog.atpic.com</a>.
     
    <t id="386">It is hosted on blogspot.com (Blogger). </t>
     
    <t id="387">News will be cross-posted on the blog:</t>
     
    <t id="388">This will allow Atpic community to leave comments about the new features.</t>
     
    </news>


    <news date="2007-08-15">
    <t id="382">Two new resolutions of image files are now available: 350 pixels and 70 pixels.</t>
     
    <t id="383">Do you like the new Atpic home page look?</t>
     
    <t id="384">We have used those two new formats.</t>
     
    </news>

    <news date="2007-08-15">
    <t id="379">The FTP credentials have been simplified:</t>
     
    <t id="380">The username and password used to log into your FTP server are now the same as the username and password used to log into your web account mangement page.</t>
     
    <t id="381">Please keep in mind we have several FTP servers and that if you try to connect to a FTP server your acount is not associated with, the login will fail.</t>
   
     
    </news>


    <news date="2007-05-19">
    <t id="373">To better serve Atpic users, a new server has been added to Atpic cluster.</t>
     
    <t id="374">Users on the server user1.atpic.com have been moved it this new server called user2.atpic.com.</t>
     
    <t id="375">This should be transparent to users except for FTP transfers.</t>
     
    <t id="376">To upload documents by FTP, those users should now use user2.atpic.com as FTP server.</t>

     
    <t id="377">This information is reminded in each account in the FTP tab.</t>
     
    <t id="378">Please do not hesitate to contact us if you have questions about this move.</t>

     
    </news>


    <news date="2007-05-10">
    <b>
    <t id="368">The interface to move mutiple pictures uploaded by FTP into a gallery has bee made more robust.</t>
    </b>
     
    <t id="369">The job of generating the thumbnails for each picture is now a process running in background.</t>
     
    <t id="370">This is to avoid timeout issues when resizing a large number of pictures.</t>
     
     
<t id="372">You can now select hundreds of pictures in your FTP zone, press the submit button and go peacefully to have your cup of tea or even take more pictures!</t>
     
    </news>




    <news date="2007-04-19">
    <t id="365">The tree navigation has been improved.</t>
     
    <t id="366">Now, thumbnails for subgalleries are shown in the prent galeries.</t>
     
    <t id="367">When a gallery has several children and is itself child of another gallery, the thumbnail in that top gallery corresponds to the picture with the highest priority.</t>
     
    </news>


    <news date="2007-04-02">
    <t id="364">You can now create subdirectories in your FTP zone and load the documents from those subdirectories into your galleries.</t>
     
    </news>




    <news date="2007-02-09">
    <t id="362">You can now choose between the Google and Yahoo! API to view the world maps of Atpic pictures.</t>
     
    <t id="363">The two maps can be accessed at:</t>
    <br/> 
     <a href="http://maps.atpic.com/map.php?api=yahoo">http://maps.atpic.com/map.php?api=yahoo</a>
    <br/> 
     <a href="http://maps.atpic.com/map.php?api=google">http://maps.atpic.com/map.php?api=google</a>
    <br/> 

    </news>


    <news date="2007-01-11">
    <t id="355">A new tool to get the latitude and longitude of a point on the Earth is available at:</t>
     
     <a href="http://atpic.com/map_helper_yahoo.html">http://atpic.com/map_helper_yahoo.html</a>

    <br/> 
    <t id="356">It is based on the Yahoo! Maps API and covers more countries than the Google Maps version available at:</t>
     
     <a href="http://atpic.com/map_helper.html">http://atpic.com/map_helper.html</a>

    </news>
    


    <news date="2006-12-27">
    <t id="350">Geotagging of pictures is available on Atpic!</t>
     
     
    <a href="http://faq.atpic.com/$setlang#geo">
    <t id="351">Click here for more information.</t>
    </a>
     
    <t id="354">Or go directly to the maps:</t>
     
   
    <a href="http://maps.atpic.com">
    <b>http://maps.atpic.com</b>
    </a>!
    </news>
    
"""





def news_old():
    
    return """
    <news date="2006-12-27">
    <t id="352">Two Google groups have been opened to allow you to discuss about Atpic.com.</t>
     
     
    <a href="http://faq.atpic.com/$setlang#geo">
    <t id="353">Groups are detailed in the FAQ.</t>
    </a>
     

    </news>
    



    <news date="2006-12-03">
    <t id="347">Surfers viewing your documents can now choose wether they want to see the document's tags or not.</t>
     
    <t id="348">This choice is saved into a cookie;</t>
     
    <t id="349">The default behaviour is to hide the tags.</t>
    </news>





    <news date="2006-11-12">
    <b><t id="341" topurl="http://top.atpic.com">The ::topurl;; uses a new popularity algorithm.</t></b>
     

    <a href="http://faq.atpic.com/$setlang#popularity">
    <t id="342">To learn how to improve the popularity of your pictures, read the popularity FAQ.</t>
    </a>
    
    </news>





    <news date="2006-11-11">
    <t id="343">The search engine is now powered by the tag index.</t>
     
    <t id="344">This increases the speed of the search a lot.</t>
     
    
    </news>

    <news date="2006-11-11">
    <t id="345">The files uploaded by FTP are now sorted alphabetically.</t>
     
    <t id="346">They were before ordered by time of upload causing random ordering in the gallery.</t>
     
    
    </news>




    <news date="2006-11-10">
    <t id="337">We are beginning to get famous! ;)</t>
     
    <t id="338">Captology.tv dedicates an article to three major picture sharing sites, including Atpic.com:</t>
     
    <a href="http://captology.tv/node/169">http://captology.tv/node/169</a>
    </news>


    <news date="2006-10-28">
    
    <t id="325">A visit counter has been released.</t>
     
    <t id="326">Every artist, gallery and picture has now a hit counter.</t>
     
    <t id="327">The counters are incremented by one each time the correponding page is loaded with a javascript aware browser.</t>

    </news>


    <news date="2006-10-27">
    
    <t id="319">Tags can now be sorted alphabetically.</t>
     
    <t id="320">Tags sorted alphabetically are found at:</t>
    //<pre>
     
    <a href="http://alphatag.atpic.com/">alphatag.atpic.com</a>;
    //</pre>
     
    <t id="321">Tags sorted by frequency are found at:</t>
     
    //<pre>
    <a href="http://tag.atpic.com/">tag.atpic.com</a>
    //</pre>
    </news>





    <news date="2006-10-27">
    
    <t id="322">You can now track how many hits your documents get.</t>
     
    <t id="323">We count hits to your homepage, your galleries and eah picture.</t>
     
    <t id="324">The counter value is presented by default at the bottom of the page.</t>
    
    
    </news>






    <news date="2006-10-09">
    <b>
    <t id="293">Broad folksonomy now available!</t>
    </b>
     
    <t id="292">Bookmark Atpic documents, the clever way, now!</t>
     
    <t id="291">We hope you become as exited by this new classification feature than we are here at Atpic.</t>
     
    <t id="290">And be carefull, this is not a narrow folsonomy, where only the doument owner can tag his documents like other sites propose.</t>
     
    <a href="http://faq.atpic.com/$setlang#folksonomy">
    <t id="289">You can read more about this innovating feature in our folksonomy FAQ.</t>
    </a>
     
    </news>

    <news date="2006-10-09">
    <t id="288">A new antispam solution has been released.</t>
     
    <a href="http://faq.atpic.com/$setlang#captcha">
    <t id="287">For more details please see our CAPTCHA FAQ.</t>
    </a>
    </news>




    <news date="2006-06-06">
    <t id="282">The parallelized code has been released.</t>
     
    <t id="283">Indeed, due to Atpic success, one computer, even large was not enough to serve store all the data.</t>
     
    <t id="284">All new accounts are now opened on the new server.</t>
     
    <t id="285">To store using HTTP you still need to log in into your account at the usual page.</t>
    <a href="http://atpic.com">http://atpic.com</a>. 
    <t id="286">For FTP uploads, you need to use the connection settings given in your atpic account management page.</t>
     
    <t id="276">If you find a problem with the new features or need more information, do not hesitate to contact us.</t>
     
    </news>


    <news date="2006-05-18">
    <t id="279">A tool that generates thumbnail for each style has been installed.</t>
<t id="280">This should make the choice of the style much easier.</t>
<t id="281">The up to date lists of styles are available here:</t>
    <a href="http://atpic.com/style_list.php?section=css">CSS</a>
    , 
    <a href="http://atpic.com/style_list.php?section=template">template</a>
    , 
    <a href="http://atpic.com/style_list.php?section=skin">skin</a>
     
    </news>





    <news date="2006-05-12">
    <b>
    <t id="267">Big news for Atpic:</t>
    </b>
     
    <t id="268">After a long development period, the styling features are out.</t>
     
    <t id="269">You can now define your own CSS and cascade sevral sheets on one page.</t>
     
    <t id="270">Using Atpic templates, you can present and structure the HTML code ectly as you.</t>
     
    <t id="271">The combination of flexible CSS and template transforms Atpic in one of the most configurable picture and video hosting sites of the market.</t>
     
    <t id="272">More information about styling, CSS and templates can be found below:</t>
     

    <ul>

     <li>
     <a href="http://atpic.com/faq.php?#styling"><t id="273">Styling</t></a>
    </li>


     <li>
     <a href="http://atpic.com/faq.php?#css"><t id="274">CSS</t></a>
    </li>


     <li>
     <a href="http://atpic.com/faq.php?#template"><t id="275">Templates</t></a>
     </li>
     
     

     
     </ul>
     
     
     
     <t id="276">If you find a problem with the new features or need more information, do not hesitate to contact us.</t>
      
     </news>
     
     
     <news date="2006-05-12">
     <t id="277">Atpic now serves the pages in XHTML 1.1 format with a XML header to browsers supporting this format (like Mozilla, Firefox and konqueror).</t>
      
     <t id="278">Atpic continue to serve pages in HTML 4.01 Transitional  format to other browsers (like IE 6).</t>
      
     </news>
     
     
     

     <news date="2006-01-22">
     <t id="265">Atpic has now its favicon!;)</t>
      
     </news>
     
     
     <news date="2006-01-22">
     <t id="261">The way the automatic resize engine works has been changed:</t>
      
     <t id="262">Now, images need to be 20% larger than the target resolution to trigger the automatic scaling.</t>
      
     <t id="263">For instance, before, when you uploaded a 610x406 pixel image, a second image with size 600x400 was created.</t>
      
     <t id="264">Now, you will need to upload a image whose longest side is longer than 720 pixels to trigger the scaling down to 600 pixels.</t>
      
     <t id="266">This will avoid storing two images with almost the same resolution.</t>
     </news>
     
     
     <news date="2006-01-07">
     <t id="259">All pages contains now an automatic javascript preload script.</t>
      
     <t id="260">This should make viewing successive pages more pleasant.</t>
     </news>
     
     
     <news date="2006-01-07">
     <t id="258">The top voted pictures are available at the following address:</t>
      
     
     <a href="http://top.atpic.com">http://top.atpic.com</a>
     </news>
     
     
     <news date="2006-01-02">
     <t id="257">The comment written in the EXIF UserComments field is now inserted in Atpic picture description field.</t>
      
    </news>
    

    <news date="2005-12-28">
    <t id="256">Websurfers can now rate the images on atpic.</t>
     
    </news>


    <news date="2005-12-25">
    <t id="253">Un new frame extraction tool has been installed.</t>
     
    <t id="254">More codecs are now supported.</t>
     
    <t id="255">You can now upload your videos in WMV (ASF) format.</t>
    </news>


    <news date="2005-12-11">
    <t id="252">Statistics about cameras used to take picture hosted on Atpic are now available at this address:</t>
     <a href="http://atpic.com/camera.php?">http://atpic.com/camera.php</a>
    </news>


    <news date="2005-12-03">
    <t id="250">The image display speed in a slide show can now be changed.</t>
     
    </news>
    
    
    <news date="2005-12-03">
    <t id="251">In the gallery properties, an option is now available to decide if individual pictures need to be automatically framed, as in the gallery pages, or not.</t>
     
    </news>
    
    
    <news date="2005-11-30">
    <t id="247">Galleries can now be viewed  in a slide show.</t>
     
    <t id="248">For a better viewing experience, images are prefetched during the show.</t>
     
    <a href="http://atpic.com/faq.php?#slideshow">
    <t id="249">More information can be found in the FAQ.</t>
    </a>
    </news>
    

    <news date="2005-11-20">
    <t id="244">The user home page can now be presented using various CSS style sheets.</t>
     
    <t id="245">User can choose between two page layouts and numerous style sheets.</t>
     
    <t id="246">If you have created a new style you would to use, just contact us and will will make them available to all Atpic users.</t>
    </news>


    <news date="2005-11-20">
    <t id="242">The number of direct links to other pictures from a picture presentation page has been limited to 10.</t>
     
    <t id="243">This should improve the presentation of pictures beloging to galleries that contain a lot of pictures.</t>
    </news>
    
    
    <news date="2005-11-16">
    <t id="240">Users can update and delete the comments made about their work.</t>
     
    <t id="241">Registered users who have posted a comment about another member's work can now update or delete it.</t>
    </news>


    <news date="2005-11-12">
    <t id="237">The forum and comment pages have been reformatted: comments for photographers now includes also comments about the galleries and pictures of the photographer.</t>
     
    <t id="238">Comments for a gallerie now includes also comments about the pictures in the gallerie.</t>
     
    <t id="239">Each photographer, gallery or picture identify a unique thread that can be tracked by RSS.</t>
    </news>


    <news date="2005-11-12">
    <t id="236">RSS feeds have been added to track the forums. Please look at the FAQ for more information.</t>
    </news>


    <news date="2005-11-07">
    <t id="235">Atpic provides RSS 2 feeds to read in your RSS news reader or into your blog/web site. More information about the feeds in the FAQ:</t>
     <a href="http://atpic.com/faq.php?#rss">RSS FAQ</a>
    </news>


    <news date="2005-07-09">
    <t id="230">The help and Atpic presentation pages are now regrouped into two documents : a FAQ (Frequetly Asked Questions) and a feature page.</t>
     
    <t id="233">As time goes, this help system will be updated and improved.</t>
     
    <t id="234">The links are:</t>
     
    <a href="http://atpic.com/faq.php?">
    <t id="231">Atpic FAQ</t>
    </a>, 
    
    
    <a href="http://atpic.com/features.php?">
    <t id="232">Atpic Features Page</t>
    </a>
    . 
    </news>
    

    <news date="2005-06-28">
    <t id="229">A simple search engine is now available. The form is at the top of the &quot;Atpic News&quot; paragraph.</t>
    </news>


    <news date="2005-06-23">
    <t id="228">On the <i>http://user.atpic.com</i> web site, you can now sort users by name and by id.</t>
    </news>


    <news date="2005-06-23">
    <t id="227">You can now setup your account to make it available by name and not only by ID. That is now you can refer to your home page using <i>http://mydomain.atpic.com</i> instead of using <i>http://atpic.com/MyID</i>. Existing users should go to the &quot;update data&quot; link and choose their domain.</t>
    </news>


    <news date="2005-06-06">
    <t id="226">You uploaded a picture but forgot to rotate it before on your computer?</t>

     
    <t id="225">That's not too late : Now Atpic allows you to rotate pictures from your picture management interface.</t>
     
    <a href="http://atpic.com/faq.php?#transform">
    <t id="224">More information on how to use this new feature here.</t>
    </a>
    </news>




    <news date="2005-06-06">
    <t id="223">To make the order of pictures in a gallery consisten with rotation, the default priority has been changed. Default priority was empty, now default priority is a 12 characters string containg the PicId prependended by &quot;a&quot;'s.</t>
    </news>



    <news date="2005-05-25">
    <t id="222">Deletion of an entire gallery is now possible.</t>
    </news>
    
    
    <news date="2005-05-25">
    <t id="220">You can now protect your galleries. Protected galleries can be seen only by users knowing its secret key.</t>
    </news>


    <news date="2005-05-08">
    <t id="221">The number of rows and columns of thumbnails for gallery pages can now be modified using the rows and columns paramters.</t>
    </news>


    <news date="2005-04-18">
    <t id="219">Due to a registrar move, some DNS issues are expected this week. In the case your computer can not resolve the atpic.com domain, just enter our IP address 69.93.100.234 in your local &quot;hosts&quot; file. We apologize for the inconvenience.</t>
    </news>


    <news date="2005-04-15">
    <b><t id="217">NOW you can upload VIDEOS!</t></b> 
    <t id="218">Atpic video hosting solution is available for testing</t>
    http://atpic.com/faq.php?#video
    </news>
    

    <news date="2005-04-06">
    <t id="214">The URL naming convention for direct access to an image has been changed</t>
<t id="215">To access directly to the JPEG file with ID picID, just go to http://raw.atpic.com/picID.</t>
<t id="216">More details in the subscription page.</t>
    </news>


    <news date="2005-03-25">
    <b><t id="212">The new ftp service is open!</t></b>


<t id="213">It allows you to upload easyly several files at one time</t>
http://atpic.com/faq.php?#ftp

    </news>


    <news date="2005-02-07">
    <t id="211">A link to open a session by email has been added for those who forget their password.</t>
    </news>


    <news date="2005-02-06">
    <t id="210">The <b>emails</b> sent by Atpic are now Unicode encoded. This allows accents and non latin alphabet based languages (like Russian, Greek, Chinese, etc...).</t>
    </news>


    <news date="2004-11-27">
    <t id="207">The links to the other pictures of a picture page are now located bellow the picture.</t>

<t id="208">All comments are now moved to a special site:</t>

<a href="http://forum.atpic.com">forum.atpic.com</a>
    </news>


    <news date="2004-07-27">
    <t id="205">Internationalization work is going well:</t>

<t id="206">See the French, Spanish, German and Dutch versions:</t>

<a href="http://atpic.com/fr">http://atpic.com/fr</a>, <a href="http://atpic.com/es">http://atpic.com/es</a>, <a href="http://atpic.com/de">http://atpic.com/de</a>, <a href="http://atpic.com/nl">http://atpic.com/nl</a>. 
    </news>


    <news date="2004-07-25">
    <t id="203">ATPIC NEEDS YOU! The internationalization tool is now available!</t>
    <a href="http://atpic.com/faq.php?#wiki" target="helpwiki">
<t id="204">Learn how you can participate to the development of Atpic</t></a>
    </news>


    <news date="2004-07-16">
    <t id="202">Now gallery.atpic.com and pic.atpic.com show the latest galleries and pictures first.</t>
    </news>


    <news date="2004-06-22">
    <t id="201">As long as this site remains free, the web space is unlimited for all accounts!</t>
    </news>


    <news date="2004-06-10">
    <t id="200">You can now sort your galleries and pictures using the <i>priority</i> field.</t>
    </news>

"""