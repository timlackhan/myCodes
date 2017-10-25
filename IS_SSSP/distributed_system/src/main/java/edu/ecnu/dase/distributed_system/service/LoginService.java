package edu.ecnu.dase.distributed_system.service;



import java.awt.print.Printable;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.apache.http.protocol.HttpContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestParam;


import edu.ecnu.dase.distributed_system.dao.LoginRepository;
import edu.ecnu.dase.distributed_system.entity.course;
import edu.ecnu.dase.distributed_system.entity.student;
import net.sf.ezmorph.array.IntArrayMorpher;

@Service
public class LoginService {

	@Autowired
	private LoginRepository loginRepo;
	
	
	public Integer loginStudent(@RequestParam("name") String name,@RequestParam("pwd") String pwd,HttpSession session) {
		student s=loginRepo.findStudent(name,pwd);
		if(s==null){
			return 0;
		}else{
			session.setAttribute("name", name);
			
			return 1;
		}
	}
	
	public Integer registerStudent(@RequestParam("name") String name,@RequestParam("pwd") String pwd){
		student s = new student();
		s.setName(name);
		s.setPwd(pwd);
		loginRepo.save(s);
		return 1;
	}

	public String getStudentName(HttpSession session) {
		return (String) session.getAttribute("name");
	}

	public List<String> getClassList(HttpSession session) {
		List<String> coursesName = new ArrayList<String>();
		String name = (String) session.getAttribute("name");
		int sid=loginRepo.findStudentId(name);
		List<Integer> coursesId=  loginRepo.getClassList(sid);
		
		Iterator<Integer> itr = coursesId.iterator(); 
		while(itr.hasNext()){  
            int cid = itr.next();
            coursesName.add(loginRepo.findCourseName(cid));
        }  
		
		return coursesName;
	}

	public List<String> getUnchoosedClasses(HttpSession session) {
		List<String> unchoosedCoursesName = new ArrayList<String>();
		List<Integer> totalClasses=loginRepo.findTotalClasses();
		String name = (String) session.getAttribute("name");
		int sid=loginRepo.findStudentId(name);
		List<Integer> coursesId=  loginRepo.getClassList(sid);
		totalClasses.removeAll(coursesId);
		
		Iterator<Integer> itr = totalClasses.iterator(); 
		while(itr.hasNext()){  
            int cid = itr.next();
            unchoosedCoursesName.add(loginRepo.findCourseName(cid));
        }  
		return unchoosedCoursesName;
	}

	public void chooseClasses(String[] courses, HttpSession session) {
		String name = (String) session.getAttribute("name");
		int sid=loginRepo.findStudentId(name);
		for(int i=0;i<courses.length;i++){
			loginRepo.chooseClasses(loginRepo.findCourseId(courses[i]),sid);
		}
	}
	
	
}
