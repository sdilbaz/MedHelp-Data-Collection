# MedHelp-Data-Collection
Python script for collection of posts and responses in MedHelp

MedHelp website can be used to collect medical questions and conversations in a medical context. The python code supplied here collects the conversations as XML trees which can be used for further processing.

The script first collects the links to communities by visiting forum list page on medhelp. For each forum, all of the links for posts are stored. After the links have been extracted, each post is visited and the post is stored as an XML tree. A sample XML tree extracted through this process is given below.

<div class="highlight highlight-text-xml"><pre>&lt;?<span class="pl-ent">xml</span><span class="pl-e"> version</span>=<span class="pl-s"><span class="pl-pds">"</span>1.0<span class="pl-pds">"</span></span><span class="pl-e"> encoding</span>=<span class="pl-s"><span class="pl-pds">"</span>UTF-8<span class="pl-pds">"</span></span>?&gt;
&lt;<span class="pl-ent">post</span>&gt;
  &lt;<span class="pl-ent">post_fields</span>&gt;
  &lt;/<span class="pl-ent">post_fields</span>&gt;
  &lt;<span class="pl-ent">response</span> <span class="pl-e">resp_id</span>=<span class="pl-s"><span class="pl-pds">"</span>0<span class="pl-pds">"</span></span>&gt;
  &lt;/<span class="pl-ent">response</span>&gt;

&lt;/<span class="pl-ent">post</span>&gt;</pre></div>

The root of the XML tree is contains relevant information from the post such as the link to post, title of the post, username of the poster, link to the poster profile if available, time of posting, and the post body.

If there is a response to the post,  the XML trees will include the responses with information such as the username, the link to the user profile if available, time of posting, and the response body.

