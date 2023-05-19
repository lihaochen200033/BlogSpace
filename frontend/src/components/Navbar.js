import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AUTH_TOKEN } from '../constants';

function Navbar() {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log(token);

    const Navigate = useNavigate();

    const Clear = () => {
        localStorage.removeItem(AUTH_TOKEN);
        Navigate("/login");
    }


    return (
        <div className="Navbar">
            <Link className="brand" to="/login">
                BlogSpace
            </Link>
            {token && <span><Link to="/home">Home Page</Link></span>}

            {token && <span className="menu"><Link to="/createpost">Add Posts</Link></span>}

            {!token &&
                <>
                    <span><Link to="/login">Login</Link></span>
                    <span><Link to="/register">Register</Link></span>
                </>
            }
            {token &&
                <>
                    <span onClick={Clear} style={{ color: 'white' }}>Logout</span>
                </>
            }
        </div>
    )
}

export default Navbar;
