package edu.ecnu.dase.distributed_system.web;

import java.io.IOException;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.http.protocol.HttpContext;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import edu.ecnu.dase.distributed_system.dao.LoginRepository;
import edu.ecnu.dase.distributed_system.entity.student;
import edu.ecnu.dase.distributed_system.service.LoginService;
import net.sf.json.JSONArray;

@RestController
@RequestMapping("/login")
public class LoginController {

	@Autowired
	private LoginService loginService;
	
	
	@RequestMapping("/login")
	public Integer loginStudent(@RequestParam("name") String name,@RequestParam("pwd") String pwd,HttpSession session) {
		return loginService.loginStudent(name, pwd,session);
	}
	
	@RequestMapping("/getName")
	public String getStudentName(HttpSession session) {
		return loginService.getStudentName(session);
	}
	
	@RequestMapping("/register")
	public Integer registerStudent(@RequestParam("name") String name,@RequestParam("pwd") String pwd){
		return loginService.registerStudent(name, pwd);
	}

	@RequestMapping("/getList")
	public List<String> getClassList(HttpSession session){
		return loginService.getClassList(session);          
	}
	
	@RequestMapping("/choose")
	public List<String> getUnchoosedClasses(HttpSession session){
		return loginService.getUnchoosedClasses(session);
	}
	
	@RequestMapping("/unchoose")
	public ModelAndView  chooseClasses(HttpServletRequest request,HttpSession session,HttpServletResponse response) throws IOException{
		String[] courses=(String[])request.getParameterValues("courses");
		loginService.chooseClasses(courses,session);
		return new ModelAndView("redirect:http://localhost:8888/html/chooseCourse.html");
	}
}
